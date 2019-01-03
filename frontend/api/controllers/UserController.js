/**
 * UserController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const url = 'https://thymesis-memories-v3.herokuapp.com/api/Users/?format=json';

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
        if (typeof req.cookies.user === 'undefined') {
            return res.view('pages/signup', {user: req.cookies.user})
        } else {
            return res.redirect('/')
        }
    },

    new: (req, res) => {
        axios.post('https://thymesis-memories-v3.herokuapp.com/api/Users/', {
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

};

