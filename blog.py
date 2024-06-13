import sqlite3
from datetime import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

# Connect to the database (create a new file if it doesn't exist)
conn = sqlite3.connect('blog.db')
c = conn.cursor()

# Create the table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS posts
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT, created_at TIMESTAMP)''')
conn.commit()


def create_post(title, content):
    """Create a new blog post"""
    c.execute("INSERT INTO posts (title, content, created_at) VALUES (?, ?, ?)",
              (title, content, datetime.now()))
    conn.commit()
    print(f"{Fore.GREEN}New post created: {title}")

def list_posts():
    """List all blog posts"""
    c.execute("SELECT * FROM posts ORDER BY created_at DESC")
    posts = c.fetchall()
    if not posts:
        print(f"{Fore.YELLOW}No posts found.")
    else:
        print(f"{Fore.CYAN}Blog Posts:")
        for post in posts:
            print(f"{Fore.MAGENTA}ID: {post[0]}")
            print(f"{Fore.GREEN}Title: {post[1]}")
            print(f"{Fore.BLUE}Created at: {post[3]}")
            print(f"{Style.DIM} ---")

def view_post(post_id):
    """View a specific blog post"""
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    if not post:
        print(f"{Fore.RED}Post with ID {post_id} not found.")
    else:
        print(f"{Fore.GREEN}Title: {post[1]}")
        print(f"{Fore.YELLOW}Content: {post[2]}")
        print(f"{Fore.BLUE}Created at: {post[3]}")

def delete_post(post_id):
    """Delete a blog post"""
    c.execute("DELETE FROM posts WHERE id = ?", (post_id,))
    conn.commit()
    if c.rowcount > 0:
        print(f"{Fore.GREEN}Post with ID {post_id} has been deleted.")
    else:
        print(f"{Fore.RED}Post with ID {post_id} not found.")

def update_post(post_id):
    """Update an existing blog post"""
    c.execute("SELECT * FROM posts WHERE id = ?", (post_id,))
    post = c.fetchone()
    if not post:
        print(f"{Fore.RED}Post with ID {post_id} not found.")
        return

    print(f"{Fore.GREEN}Current Post:")
    print(f"Title: {post[1]}")
    print(f"Content: {post[2]}")

    new_title = input(f"{Fore.YELLOW}Enter the new title (leave blank to keep the current title): ").strip()
    new_content = input(f"{Fore.YELLOW}Enter the new content (leave blank to keep the current content): ").strip()

    if not new_title:
        new_title = post[1]
    if not new_content:
        new_content = post[2]

    c.execute("UPDATE posts SET title = ?, content = ? WHERE id = ?", (new_title, new_content, post_id))
    conn.commit()
    print(f"{Fore.GREEN}Post with ID {post_id} has been updated.")
    


while True:
    action = input(f"{Fore.CYAN}What would you like to do? (c){Fore.GREEN}reate{Fore.CYAN}, (l){Fore.GREEN}ist{Fore.CYAN}, (v){Fore.GREEN}iew{Fore.CYAN}, (u){Fore.GREEN}pdate{Fore.CYAN}, (d){Fore.GREEN}elete{Fore.CYAN}, or (q){Fore.GREEN}uit{Fore.CYAN}: ").lower()

    if action == 'c':
        title = input(f"{Fore.GREEN}Enter the post title: ")
        content = input(f"{Fore.GREEN}Enter the post content: ")
        create_post(title, content)

    elif action == 'l':
        list_posts()

    elif action == 'v':
        post_id = int(input(f"{Fore.GREEN}Enter the post ID: "))
        view_post(post_id)

    elif action == 'u':
        post_id = int(input(f"{Fore.GREEN}Enter the post ID to update: "))
        update_post(post_id)

    elif action == 'd':
        post_id = int(input(f"{Fore.GREEN}Enter the post ID to delete: "))
        delete_post(post_id)

    elif action == 'q':
        break

    else:
        print(f"{Fore.RED}Invalid action. Please try again.")

# Close the database connection
conn.close()