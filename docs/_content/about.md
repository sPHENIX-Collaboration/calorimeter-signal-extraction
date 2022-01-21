---
title: About
layout: base
name: about
---

# About this site

Materials on this site are and kept in the
<a href="https://www.markdownguide.org/basic-syntax/" target="_blank">Markdown Syntax</a>
which is very human-readable and economical, being quite close to plain text.
You may be familiar with this syntax if you ever had to edit README.md files on
GitHub or similar documents elsewhere. The site is built using the *static site
generator* technology, whereby a group of Markdown files are compiled into
HTML and form a cohesive site. This results in enhanced site security and performance.
Static site generation is implemented natively in the *GitHub Pages* framework i.e.
sites are automatically generated and hosted if the respective repository
is properly configured.

In addittion of text-based content there are
options to filter, transform and render data content kept in formats
such as YAML or CSV using the
<a href="https://shopify.github.io/liquid/" target="_blank">Liquid</a> template language.
This allows the developer to implement a modicum of database-like functionality without
having the actual database.

---

# Contributing to the site

## GitHub

If you are interested in contributing to this site
please <a href="{{ '/content/contact.html' | relative_url }}">contact the devloper</a>
for more information. Menu items and pages can be quickly added as needed.
Once a section is set up, creation of material amounts to editing text files
(at least in most basic cases).
GitHub has now integrated the powerful *VS Code* editor into its
web portal, which enables the users to do meaningful work e.g. modify and
create content directly in the browser, without installing any software
on their machine. Saving the content will result in automatic "commit/push"
to the GitHub repository and automatic site refresh, which may take a couple
of minutes.

## Using your machine

Optionally, the user can install the
<a href="http://jekyllrb.com/" target="_blank">Jekyll</a> web
site generator on their laptop or workstation which allows more flexibility in testing
and experimentation. Expert users can also leverage the following components of the platform:
* The <a href="https://shopify.github.io/liquid/" target="_blank">Liquid</a> template language which will help manuipulate and render structured data on web pages
* The <a href="http://getbootstrap.com/" target="_blank">Bootstrap</a> toolkit - for modifying layouts and appearance of these web pages and their behavior

Please take a look at the <a href="{{ site.github }}" target="_blank">repository</a>
to get an idea of the general organization of the data, layouts and supporing logic.
The idea is to shape the code and content in a way that is easy to navigate

---

# Managing Data
Jekyll is flexible when it comes to storing and manipulating structured data.
The data component of the site can reside in the "front matter" section of individual Markdown-formatted
files or in separate YAML (or JSON, CSV etc) data sources. The former approach works well
for small quantities of data. For scalability, it is recommended to rely mostly on dedicated data files (i.e.
files in the "<a href="{{ site.github }}/tree/master/_data" target="_blank">_data</a>" folder)
and keep the content of the front matter sections of individual MD files to a minimum.

