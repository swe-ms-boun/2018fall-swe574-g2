/**
 * UserController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const moment = require('moment');
const url = 'https://thymesis-memories-v4.herokuapp.com/api/Users/?format=json';
const postUrl = 'https://thymesis-memories-v4.herokuapp.com/api/Posts/?format=json';

module.exports = {
  
    list: (req, res) => {
        axios.get(url).then((response) => {
            return res.json(response.data);
        });
    },

    login: (req, res) => {
        axios.get(url).then((response) => {
            const users = response.data;
            console.log(users.length)
            users.forEach((user) => {
                console.log(user.username)
                if (user.username === req.query.username) {
                    if (user.user_password === req.query.password) {
                        // Here is the successful login
                        res.cookie('user', user);
                        return res.redirect('/');
                    } else {
                        return res.json('password is incorrect for the user: ' + user.username);
                    }
                }
            });
        });
    },

    signup: (req, res) => {
        return res.view('pages/signup', {user: req.cookies.user})
    },

    new: (req, res) => {
        axios.post('https://thymesis-memories-v4.herokuapp.com/api/Users/', {
            username: req.query.username,
            firstname: req.query.firstname,
            lastname: req.query.lastname,
            user_password: req.query.user_password,
            email: req.query.email,
            mobile_number: req.query.mobile_number,
            home_page: req.query.home_page,
        }).then((response) => {
            console.log(response.data)
            return res.redirect('/');
        }).catch((error) => {
            console.log(error)
            return res.json(error)
        })
    },

    logout: (req, res) => {
        res.clearCookie('user');
        return res.redirect('/');
    },

    page: (req, res) => {
        let userPosts = []
        axios.get(postUrl).then((response) => {
            let posts = response.data;
            posts.sort(function(a, b){
                var keyA = new Date(a.datetime),
                    keyB = new Date(b.datetime);
                // Compare the 2 dates
                if(keyA > keyB) return -1;
                if(keyA < keyB) return 1;
                return 0;
            });
            posts.forEach((post) => {
                post.datetime = moment(post.datetime).startOf('hour').fromNow();
                if (post.user === req.param('user')) {
                    userPosts.push(post);
                }
            })
            axios.get('https://thymesis-memories-v4.herokuapp.com/api/Users/'+ req.param('user')).then((response) => {
                let pageUser = response.data;
                return res.view('pages/user',{user: req.cookies.user, pageUser, userPosts})
            })
        })
    },

};

