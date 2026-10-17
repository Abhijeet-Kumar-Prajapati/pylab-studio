const mongoose = require('mongoose');

const postSchema = new mongoose.Schema({
    userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
    imageUrl: { type: String, required: true },
    comments: [{ userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' }, text: String }],
    likes: [{ userId: { type: mongoose.Schema.Types.ObjectId, ref: 'User' } }],
});

module.exports = mongoose.model('Post', postSchema);
