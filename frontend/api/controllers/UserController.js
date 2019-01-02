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
            users.forEach((user) => {
                if (user.username === req.query.username) {
                    if (user.user_password === req.query.password) {
                        // Here is the successful login
                        res.cookie('user', user);
                        return res.redirect('/');
                    } else {
                        return res.json('password is incorrect for the user: ' + user.username);
                    }
                } else {
                    return res.json({
                        message: 'unsuccessful login',
                    });
                }
            });
        });
    },

    logout: (req, res) => {
        res.clearCookie('user');
        return res.redirect('/');
    },

};

