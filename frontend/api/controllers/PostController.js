/**
 * PostController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const url = 'https://thymesis-memories-v2.herokuapp.com/api/Posts/'
const commentUrl = 'https://thymesis-memories-v2.herokuapp.com/api/Comments/'
const annotationUrl = 'http://thymesis-api.herokuapp.com/add/annotation/'

// http://thymesis-api.herokuapp.com/add/annotation/?id=http://thymesis.com/annotation/1&creator_id=1
//             &target={"type": "Text", "source": "http://example.org/memory1", "selector": {"type": "TextPositionSelector",
//             "start": "412", "end": "795"}}

module.exports = {

    list: (req, res) => {
        axios.get(url).then((response) => {
            return res.send(response.data);
        }).catch((error) => {
            return res.send(error);
        });
    },

    new: (req, res) => {
        if (typeof req.cookies.user !== 'undefined') {
            axios.post(url, {
                uri: req.cookies.user.home_page,
                title: req.query.title,
                summary: req.query.summary,
                body: req.query.body,
                location: req.query.lat + ':' + req.query.lng,
                type: 'text',
                votes: 0,
                user: req.cookies.user.user_id,
            }).then((response) => {
                
                return res.send(response.data);
            }).catch((error) => {
                return res.send(error);
            });
        } else {
            return res.json('please login for this');
        }
        
    },

    page: (req, res) => {
        if (typeof req.param('id') === 'undefined') {
            return res.redirect('/')
        }
        axios.get(url + req.param('id')).then((response) => {
            let memory = response.data;
            axios.get(commentUrl).then((resp) => {
                let comments = [];
                let allComments = resp.data;
                allComments.forEach((comment) => {
                    if (comment.post === memory.post_id) {
                        comments.push(comment);
                    }
                })
                return res.view('pages/memory', { memory, comments, user: req.cookies.user });
            })
            
        }).catch((error) => {
            return res.send(error);
        });
    },

    create: (req, res) => {
        return res.view('pages/create', {user: req.cookies.user});
    },

    annotate: (req, res) => {
        if (typeof req.param('id') === 'undefined') {
            return res.redirect('/')
        }
        axios.get(url + req.param('id')).then((response) => {
            let memory = response.data;
            return res.view('pages/annotate', { memory, user: req.cookies.user });
        }).catch((error) => {
            return res.send(error);
        });
    },

    newanno: (req, res) => {
        axios.put(annotationUrl,{
            target: req.query.target,
            id: req.query.id,
            creator_id: 1,
        }).then((response) =>{
            return res.json(response.data);
        }).catch((error) => {
            let x = error.data;
            return res.send(x);
        })
    },

    user: (req, res) => {
        axios.get(url).then((response) => {
            const posts = response.data;
            const userPosts = [];
            posts.forEach((post) => {   
                if (post.user === req.query.id) {
                    userPosts.push(post);
                }
            });
            return res.json(userPosts);
        });
    },

};

