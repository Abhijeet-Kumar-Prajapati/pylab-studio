const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const User = require('./models/User');
const Post = require('./models/Post');

const app = express();
app.use(express.json());

// MongoDB connection
mongoose.connect('mongodb://localhost/socialmedia', { useNewUrlParser: true, useUnifiedTopology: true })
    .then(() => console.log('Connected to MongoDB'))
    .catch((err) => console.log(err));

// Schemas live in ./models/User.js and ./models/Post.js

// Multer setup for file uploads
const upload = multer({ dest: 'uploads/' });

// Register User
app.post('/register', async (req, res) => {
    const { username, password } = req.body;
    const hashedPassword = await bcrypt.hash(password, 10);
    const newUser = new User({ username, password: hashedPassword });
    await newUser.save();
    res.status(200).json({ message: 'User registered successfully' });
});

// Login User
app.post('/login', async (req, res) => {
    const { username, password } = req.body;
    const user = await User.findOne({ username });
    if (!user) return res.status(400).json({ message: 'User not found' });

    const isValid = await bcrypt.compare(password, user.password);
    if (!isValid) return res.status(400).json({ message: 'Invalid password' });

    const token = jwt.sign({ userId: user._id }, 'your_secret_key');
    res.status(200).json({ token });
});

// Upload Post (image)
app.post('/upload', upload.single('image'), async (req, res) => {
    const { token } = req.headers;
    const { userId } = jwt.verify(token, 'your_secret_key');
    const newPost = new Post({
        userId,
        imageUrl: req.file.path,
        comments: [],
        likes: [],
    });
    await newPost.save();
    res.status(200).json({ message: 'Post uploaded successfully', post: newPost });
});

// Like Post
app.post('/like', async (req, res) => {
    const { postId } = req.body;
    const { token } = req.headers;
    const { userId } = jwt.verify(token, 'your_secret_key');

    const post = await Post.findById(postId);
    if (!post) return res.status(400).json({ message: 'Post not found' });

    const isLiked = post.likes.some((like) => like.userId.toString() === userId.toString());
    if (isLiked) {
        post.likes = post.likes.filter((like) => like.userId.toString() !== userId.toString());
    } else {
        post.likes.push({ userId });
    }

    await post.save();
    res.status(200).json({ message: isLiked ? 'Like removed' : 'Post liked', post });
});

// Comment on Post
app.post('/comment', async (req, res) => {
    const { postId, commentText } = req.body;
    const { token } = req.headers;
    const { userId } = jwt.verify(token, 'your_secret_key');

    const post = await Post.findById(postId);
    if (!post) return res.status(400).json({ message: 'Post not found' });

    post.comments.push({ userId, text: commentText });
    await post.save();
    res.status(200).json({ message: 'Comment added', post });
});

// Start server
app.listen(3000, () => {
    console.log('Server running on port 3000');
});
