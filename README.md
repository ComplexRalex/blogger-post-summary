# BloPS

Acronym(?) for *Blogger Post Summary* (idk it sounds funny). It's a Python script to extract basic information from your Blogger blog posts.

**Note**. This script requires you to provide a JSON file instead of using the actual API. For more information, read about [the limitations](#limits).

## Features

* Summarize your Blogger blog posts into a CSV file
* Generate HTML files for each post

## Requirements

* Python 3.10
* Experience using terminal/console
* Access to Google's Blogger API

## First steps

### Blog ID

Go to your Blogger posts (or entries) of the blog you want to review, and copy the large number at the end of the URL.

```txt
https://www.blogger.com/blog/posts/####################
```

Save it for later.

### Access to Google's APIs Explorer

There is an APIs Explorer for every Google service (for which it is available). For this case, we are only using [Blogger's v3 APIs Explorer](https://developers.google.com/blogger/docs/3.0/reference/posts/list) to get the post list from your blog.

### Getting the post list

Once you clicked the link above, read the first lines of the entry and click on **Try it now**. This will open up the **APIs Explorer** on your right side. Here, you can filter the list of posts as you please.

The required parameter here is **blogId**. It's time to bring your ID, *bro*.

> **Note**. I recommend you to tweak the request parameters depending on the content you want to extract. As an example, this query returns up to **10 posts** by default, but you can increase this number by changing the **maxResults** field.

After you're done doing so, click on **API key** checkbox and then **Execute**.

> **One note more**. If you want to extract *DRAFT* posts as well, you'll have to click **Google OAuth 2.0** checkbox as well due to its privacy properties. However, this requires you to **create an app in Google Cloud** (which is not that hard though, since Google is guiding you in the process).

Finally, a textbox will show up at the bottom of the drawer. This is the list of posts in **JSON format**. Copy its contents and paste them in a file with `.json` extension.

## Commands

Assuming you've already [installed Python](https://www.python.org/downloads/) and [configured a *venv*](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/), you can run the following script.

**Tip.** Whenever you are unsure how to run the command, `-h` option will be your friend!

### `get_blogger_posts_csv.py`

This script will collect very basic stuff, like `id`, `title`, `content` and `status`.

The complete command is the following:

```sh
py get_blogger_posts_csv.py --input_filename <input_filename> --output_filename <output_filename> --output_document_directory <output_document_directory>
```

All argument default options are the following:

| Argument | Default value | Description |
| - | - | - |
| `input_filename` | input/blogger_posts.json | The input JSON file containing the Blogger posts in JSON format. |
| `output_filename` | output/blogger_posts_info.csv | The output CSV file containing all info from the posts. |
| `output_document_directory` | output/blogger_posts_docs | The output directory to store HTML posts. |

**Note**. HTML posts are named after their UNIX creation timestamp.

## Limits

* As mentioned before, this script does not use the API directly. The main reason for this was the necessity to include **Google OAuth 2.0** integration in the script, which was a bit overkill for the main purpose of this repo (I just wanted to manage my posts *asap*, lol).

## Notes

The result will contain posts ordered by its UNIX timestamp ascendingly.

If there's any error with the script or this README, let me know by opening an issue, or maybe just throw me a message at my Twitter profile!
