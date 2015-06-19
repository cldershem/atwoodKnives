#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
bike_tool_notifier.py
~~~~~~~~~~~~~~~~~

Checks atwoodknives to see if the bike tool has been released.

:copyright: (c) 2015 by Cameron Dershem.
:license: see TOPMATTER
:source: github.com/cldershem/atwoodKnives
"""
import feedparser
import dateutil.parser
import smtplib
import secrets
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


TESTING = True


def get_most_recent(feed):
    post = feed.entries[0]

    return post


def is_new_post(date_string):
    if TESTING:
        return True

    start_date = dateutil.parser.parse('2015-06-19 10:34:00-04:00')
    last_date = dateutil.parser.parse(date_string)

    if last_date > start_date:
        return True
    else:
        return False


def is_bike_related(post):
    keywords = ['bike', 'bicycle', 'cycle', 'wheelman']
    if TESTING:
        keywords.append('the')

    content = post.content[0].value

    for keyword in keywords:
        if keyword in content.lower():
            return True
            break
    return False


def bike_tool_released(date, post):
    if is_new_post(date) and is_bike_related(newest_post):
        return True


def send_email(post):
    email = secrets.EMAIL_ADDRESS
    password = secrets.PASSWORD
    msg = MIMEMultipart()

    from_address = email
    to_address = email
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "Atwood released the bike tool!!!"

    body = "<a href='{}'>BIKE TOOL!!!!!</a>".format(post.link)
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(from_address, to_address, text)
    server.quit()


if __name__ == '__main__':
    url = 'http://atwoodknives.blogspot.com/feeds/posts/default'
    feed = feedparser.parse(url)
    newest_post = get_most_recent(feed)
    date = newest_post.published

    if bike_tool_released(date, newest_post):
        send_email(newest_post)
