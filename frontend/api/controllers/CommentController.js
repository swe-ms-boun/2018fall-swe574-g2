/**
 * CommentController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');

const url = 'https://thymesis-memories-v4.herokuapp.com/api/Comments/'

module.exports = {

    new: (req, res) => {
       
        axios.post(url, {
            body: req.query.comment,
            post: req.query.post,
            user: req.query.user,
        }).then((response) => {
            return res.redirect('/memory/' + req.query.post);
        }).catch((error) => {
            return res.send(error);
        });
    },

};

