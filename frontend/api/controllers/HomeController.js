/**
 * HomeController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const url = 'https://thymesis-memories-v2.herokuapp.com/api/Posts/'
const userUrl = 'https://thymesis-memories-v2.herokuapp.com/api/Users/'

module.exports = {
  
    index: (req, res) => {
        console.log('helllo')
        axios.get(url).then((response) => {
            let posts = response.data;
            return res.view('pages/homepage', { 
                user: req.cookies.user,
                posts, 
            });
        });
        
    },

};

