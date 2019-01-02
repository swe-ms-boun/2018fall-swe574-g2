/**
 * HomeController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const moment = require('moment')
const url = 'https://thymesis-memories-v3.herokuapp.com/api/Posts/'
const userUrl = 'https://thymesis-memories-v3.herokuapp.com/api/Users/'

module.exports = {
  
    index: (req, res) => {
        axios.get(url).then((response) => {
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
            });
            return res.view('pages/homepage', { 
                user: req.cookies.user,
                posts, 
            });
        });
        
    },

};

