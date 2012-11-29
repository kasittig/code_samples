import unittest

"""
Code by Karen Sittig (kasittig@mit.edu)

Goal: given a valid string of HTML, split the HTML into substrings
of valid HTML that contain at most four words.  Maintain div, paragraph,
and link tags and remove all others.

Example:

input: "<html><div><p> this is a <a><b>long</b> sentence </a> <i> that will </i> be paginated </p></div></html>"
output: ["<div> <p> this is a <a> long </a> </p> </div>", "<div> <p> <a> sentence </a> that will be </p> </div>", "<div> <p> paginated </p> </div>"]

Test cases included in the "test" function.  To test, use Python to run this file.

"""

open_tags = ["<div>", "<p>", "<a>"]
close_tags = ["</div>", "</p>", "</a>"]

def tokenize_html_string(html_string):
  """
  Splits the HTML string into either word or tag tokens.

  Takes: a string of valid HTML
  Returns: a list of tokens
  """

  tokens = []
  token = ""
  for elt in html_string:
    if elt == ">":
      tokens.append(token + ">")
      token = ""
    elif elt == " ":
      if token != "":
        tokens.append(token)
      token = ""
    elif elt == "<":
      if token != "":
        tokens.append(token)
        token = elt
      else:
        token = elt
    else:
      token += elt
  return tokens

def sanitize_html_string(tokens):
  """
  Removes unwanted tags from the list of tokens.

  Takes: a list of tokens
  Returns: a list of valid tokens (words, paragraph tags, hyperlink tags, and div tags)
  """

  sanitized_tokens = []
  for elt in tokens:
    if "<" not in elt or elt in open_tags or elt in close_tags:
      sanitized_tokens.append(elt)
  return sanitized_tokens

def split_html_string(string_to_split):

  """
  Takes a string of valid HTML and returns a list of strings of valid HTML.

  Each sublist of valid HTML contains four or fewer words.
  """

  tokens = tokenize_html_string(string_to_split)

  tokens = sanitize_html_string(tokens)

  word_count = 0
  word_lists = []
  curr_word = []

  # split the list of tokens into sublists of tokens.
  # each sublist contains at most 4 words
  for elt in tokens:
    curr_word.append(elt)
    if "<" not in elt:
      word_count += 1
    if word_count == 4:
      word_lists.append(curr_word)
      word_count = 0
      curr_word = []
  if word_count > 0:
    word_lists.append(curr_word)

  # now, fix the tags in the substrings.
  # starting at the beginning, find the open tags.
  # close them in each substring until we find a close
  # tag.  then, we're done.

  # the opened tags that still need to be closed.  initially,
  # there are none
  orphaned_tags = []

  full_html = []

  for sublist in word_lists:
    # append the missing open tags to the beginning of the string
    sublist = orphaned_tags + sublist
    orphaned_tags = []
    for elt in sublist:
      # if we have an open tag but not a close tag
      if elt in open_tags and close_tags[open_tags.index(elt)] not in sublist:
        # the tag is still orphaned
        orphaned_tags.append(elt)
        # also, it needs to be closed
        sublist.append(close_tags[open_tags.index(elt)])

    full_html.append(sublist)

  html_strings = []

  # flatten the list of tokens into a string
  for elt in full_html:
    html_strings.append(" ".join(elt))
  
  return html_strings	

# some test cases for each function

class TestFunctions(unittest.TestCase):

  def setUp(self):
    # original test case
    self.test1 = "<html><div><p> this is a <a><b>long</b> sentence </a> <i> that will </i> be paginated </p></div></html>"
    # contains one invalid HTML tag
    self.test2 = "<html><div> this <b> short </b> sentence also needs to be split </div></html>"
    # doesn't need to change at all
    self.test3 = "<div> a short sentence </div>"

  def test_tokenize(self):
    self.assertEquals(tokenize_html_string(self.test1), ["<html>", "<div>", "<p>", "this", "is", "a", "<a>", "<b>", \
                                                       "long", "</b>", "sentence", "</a>", "<i>", "that", "will", \
                                                       "</i>", "be", "paginated", "</p>", "</div>", "</html>"])
        
    self.assertEquals(tokenize_html_string(self.test2), ["<html>", "<div>", "this", "<b>", "short", "</b>", "sentence", \
                                                       "also", "needs", "to", "be", "split", "</div>", "</html>"])
    self.assertEquals(tokenize_html_string(self.test3), ["<div>", "a", "short", "sentence", "</div>"])

  def test_sanitize(self):
    tokens_1 = tokenize_html_string(self.test1)
    tokens_2 = tokenize_html_string(self.test2)
    tokens_3 = tokenize_html_string(self.test3)

    self.assertEquals(sanitize_html_string(tokens_1), ["<div>", "<p>", "this", "is", "a", "<a>", "long", "sentence", \
                                                       "</a>", "that", "will", "be", "paginated", "</p>", "</div>"])
    self.assertEquals(sanitize_html_string(tokens_2), ["<div>", "this", "short", "sentence", \
                                                       "also", "needs", "to", "be", "split", "</div>"])
    self.assertEquals(sanitize_html_string(tokens_3), ["<div>", "a", "short", "sentence", "</div>"])

  def test_all(self):
    self.assertEquals(split_html_string(self.test1), ["<div> <p> this is a <a> long </div> </p> </a>", \
                                                      "<div> <p> <a> sentence </a> that will be </div> </p>", \
                                                      "<div> <p> paginated </p> </div>"])#!/usr/bin/env python
    self.assertEquals(split_html_string(self.test2), ["<div> this short sentence also </div>", \
                                                      "<div> needs to be split </div>"])
    self.assertEquals(split_html_string(self.test3), ["<div> a short sentence </div>"])

if __name__ == "__main__":
  suite = unittest.TestLoader().loadTestsFromTestCase(TestFunctions)
  unittest.TextTestRunner(verbosity=2).run(suite)
