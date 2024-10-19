import json
import csv
import argparse
import os
from datetime import datetime


# Default arguments
default_input_filename = "input/blogger_posts.json"
default_output_filename = "output/blogger_posts_info.csv"
default_output_directory = "output/blogger_posts_docs"


def verify_file_directory(output_filename):
    output_directory = os.path.dirname(output_filename)

    if output_directory != '' and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return


def verify_directory(output_directory):
    if output_directory != '' and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    return


def extract_post_info(post):
    post_id = post["id"]
    post_title = post["title"]
    post_content = f"{post["content"].replace("\n", " ")},"
    post_url = post["url"]
    post_status = post["status"]
    post_date = post["published"]
    post_unix_timestamp = datetime.fromisoformat(post_date).timestamp()
    post_updated = post.get("updated")
    post_unix_updated_timestamp = datetime.fromisoformat(post_updated).timestamp()
    post_author = post["author"].get("displayName")

    post_labels = post.get("lables")
    if post_labels is not None and len(post_labels) > 0:
        post_labels = ", ".join(sorted(post_labels))

    return {
        "post_id": post_id,
        "post_title": post_title,
        "post_content": post_content,
        "post_url": post_url,
        "post_status": post_status,
        "post_date": post_date,
        "post_unix_timestamp": post_unix_timestamp,
        "post_updated": post_updated,
        "post_unix_updated_timestamp": post_unix_updated_timestamp,
        "post_author": post_author,
        "post_labels": post_labels
    }


def extract_post_html_content(post):
    post_unix_timestamp = datetime.fromisoformat(post["published"]).timestamp()

    return {
        "post_unix_timestamp": post_unix_timestamp,
        "post_raw_content": post["content"],
    }


def main():
    parser = argparse.ArgumentParser(description="Extract important post information from a Blogger JSON posts file.")
    parser.add_argument(
        "--input_filename",
        type=str,
        help="The input JSON file containing the Blogger posts in JSON format.",
        default=default_input_filename,
    )
    parser.add_argument(
        "--output_filename",
        type=str,
        help="The output CSV file containing all info from the posts.",
        default=default_output_filename,
    )
    parser.add_argument(
        "--output_document_directory",
        type=str,
        help="The output directory to store HTML posts.",
        default=default_output_directory,
    )

    args = parser.parse_args()

    input_filename = args.input_filename
    output_filename = args.output_filename
    output_document_directory = args.output_document_directory

    verify_file_directory(output_filename)
    verify_directory(output_document_directory)

    data = []

    try:
        with open(input_filename, "r", encoding="utf-8") as file:
            object = json.load(file)
            data = object["items"]

    except Exception as e:
        print(f"An error occurred when trying to open input file {input_filename}: {e}")
        return 1

    all_post_info = []
    all_html_posts = []

    for post in data:
        post_info = extract_post_info(post)
        all_post_info.append(post_info)

        post_content = extract_post_html_content(post)
        all_html_posts.append(post_content)

    all_post_info.sort(key=lambda post: post["post_unix_timestamp"])

    try:
        with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
            fieldnames = [
                "post_id",
                "post_title",
                "post_content",
                "post_url",
                "post_status",
                "post_date",
                "post_unix_timestamp",
                "post_updated",
                "post_unix_updated_timestamp",
                "post_author",
                "post_labels",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for info in all_post_info:
                writer.writerow(info)

    except Exception as e:
        print(f"An error ocurred when trying to write to ouput file {output_filename}: {e}")
        return 1

    for html in all_html_posts:
        filename = os.path.join(output_document_directory, str(int(html["post_unix_timestamp"])))

        try:
            with open(f"{filename}.html", "w", encoding="utf-8") as file:
                file.write(html["post_raw_content"])

        except Exception as e:
            print(f"An error ocurred when trying to write the HTML file {filename}: {e}")
            return 1

    print(f"Process finished (number of posts extracted: {len(all_post_info)}). Check out your file at {output_filename}!")

    return 0


if __name__ == "__main__":
    main()
