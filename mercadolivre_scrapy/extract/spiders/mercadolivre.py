#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
MercadoLivre Scraper

This spider crawls MercadoLivre product listings for frost-free refrigerators,
extracting product details such as brand, name, pricing, and review information.
The spider is limited to crawl a maximum of 20 pages by default.

Usage:
    scrapy crawl mercadolivre -o ../data/data.json
"""

import scrapy


class MercadolivreSpider(scrapy.Spider):
    """
    Scrapy spider to scrape product data from Mercado Livre's frost-free refrigerator listings.

    This spider navigates through multiple pages of product listings and extracts details
    such as brand, name, prices, review ratings, and review counts.

    Attributes:
        name (str): Spider identifier used by Scrapy
        allowed_domains (list): Restricts crawling to specified domains
        start_urls (list): Initial URL(s) to begin crawling
        page_count (int): Counter for tracking current page number
        max_pages (int): Maximum number of pages to crawl
    """

    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/geladeira-frost-free"]

    # Pagination control
    page_count = 1
    max_pages = 20

    def parse(self, response):
        """
        Parse product information from MercadoLivre search results page.

        Args:
            response (scrapy.http.Response): HTTP response from the website

        Yields:
            dict: Product information including brand, name, pricing, and reviews
            scrapy.Request: Request to the next page if available and within limits
        """
        # Select all product containers on the page
        products = response.css("div.ui-search-result__wrapper")

        # Extract data for each product
        for product in products:
            yield {
                "brand": product.css("span.poly-component__brand::text").get(),
                "name": product.css("h3.poly-component__title-wrapper a::text").get(),
                "old_price": product.css(
                    "s.andes-money-amount.andes-money-amount--previous.andes-money-amount--cents-comma span.andes-money-amount__fraction::text"
                ).get(),
                "new_price": product.css(
                    "div.poly-price__current span.andes-money-amount__fraction::text"
                ).get(),
                "review_rating_number": product.css("span.poly-reviews__rating::text").get(),
                "review_amount": (
                    product.css("span.poly-reviews__total::text").get(default="0") or "0"
                ).strip("()"),  # Ensures `None` does not cause an error
            }

        # Check if the maximum number of pages has been reached
        if self.page_count < self.max_pages:
            next_page = response.css(
                "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"
            ).get()
            # Extract the URL for the next page
            if next_page is not None:
                self.page_count += 1
                # Follow the next page and recursively call the parse method
                yield response.follow(next_page, callback=self.parse_next_pages)

    def parse_next_pages(self, response):
        """
        Parse product information from MercadoLivre search results page.

        Args:
            response (scrapy.http.Response): HTTP response from the website

        Yields:
            dict: Product information including brand, name, pricing, and reviews
            scrapy.Request: Request to the next page if available and within limits
        """
        # Select all product containers on the page
        products = response.css("div.ui-search-result__wrapper")

        # Extract data for each product
        for product in products:
            yield {
                "brand": product.css(
                    "span.ui-search-item__brand-discoverability.ui-search-item__group__element::text"
                ).get(),
                "name": product.css(
                    "h2.ui-search-item__title.ui-search-item__group__element a::text"
                ).get(),
                "old_price": product.css(
                    "s.andes-money-amount span.andes-money-amount__fraction::text"
                ).get(),
                "new_price": product.css(
                    "div.ui-search-price__second-line span.andes-money-amount__fraction::text"
                ).get(),
                "review_rating_number": product.css(
                    "span.ui-search-reviews__rating-number::text"
                ).get(),
                "review_amount": (
                    product.css("span.ui-search-reviews__amount::text").get(default="0") or "0"
                ).strip("()"),  # Ensures `None` does not cause an error
            }

        # Check if the maximum number of pages has been reached
        if self.page_count < self.max_pages:
            next_page = response.css(
                "li.andes-pagination__button.andes-pagination__button--next a::attr(href)"
            ).get()
            # Extract the URL for the next page
            if next_page is not None:
                self.page_count += 1
                # Follow the next page and recursively call the parse method
                yield response.follow(next_page, callback=self.parse_next_pages)
