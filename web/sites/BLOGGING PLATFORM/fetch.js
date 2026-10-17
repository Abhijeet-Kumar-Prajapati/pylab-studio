// Front end for the blog platform: loads posts from the API and renders them.
async function fetchPosts() {
    const response = await fetch('/posts');
    const posts = await response.json();
    const postList = document.getElementById('post-list');
    posts.forEach(post => {
        const postElement = document.createElement('div');
        postElement.innerHTML = `<h2>${post.title}</h2><p>${post.content}</p>`;
        postList.appendChild(postElement);
    });
}

document.addEventListener('DOMContentLoaded', fetchPosts);