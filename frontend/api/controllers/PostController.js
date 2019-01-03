/**
 * PostController
 *
 * @description :: Server-side actions for handling incoming requests.
 * @help        :: See https://sailsjs.com/docs/concepts/actions
 */

const axios = require('axios');
const moment = require('moment');


const options =
    { // This is the usual stuff
    adapter: require('skipper-better-s3')
    , key: process.env.S3_KEY
    , secret: process.env.S3_SECRET
    , bucket: 'thymesis-aws'
    , region: 'us-east-1'
    , s3params:
    { ACL: 'public-read'
    }
    , onProgress: progress => sails.log.verbose('Upload progress:', progress)
    }


const url = 'https://thymesis-memories-v3.herokuapp.com/api/Posts/'
const commentUrl = 'https://thymesis-memories-v3.herokuapp.com/api/Comments/'
const annotationUrl = 'http://thymesis-api.herokuapp.com/add/annotation/'

module.exports = {

    list: (req, res) => {
        axios.get(url).then((response) => {
            return res.send(response.data);
        }).catch((error) => {
            return res.send(error);
        });
    },

    upload: (req, res) => {
        req.file('image').upload(options, (err, filesUploaded) => {
          if (err) return res.serverError(err);
          return res.json({ file: filesUploaded[0].extra.Location});
        });
      },

    new: (req, res) => {
        console.log(req.query);
        console.log(req.cookies.user.home_page)
        console.log(req.cookies.user.user_id)
        if (typeof req.cookies.user !== 'undefined') {
            axios.post(url, {
                uri: req.cookies.user.home_page,
                title: req.query.title,
                summary: req.query.summary,
                body: req.query.body,
                location: req.query.lat + ':' + req.query.lng,
                image_url: req.query.image_url,
                votes: 0,
                user: req.cookies.user.user_id,
            }).then((response) => {
                console.log(response.data);
                return res.redirect('/memory/' + response.data.post_id);
            }).catch((error) => {
                console.log(error)
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
            memory.datetime = moment(memory.datetime).startOf('hour').fromNow();
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

    annotateimg: (req, res) => {
        if (typeof req.param('id') === 'undefined') {
            return res.redirect('/')
        }
        axios.get(url + req.param('id')).then((response) => {
            let memory = response.data;
            return res.view('pages/annotateimg', { memory, user: req.cookies.user });
        }).catch((error) => {
            return res.send(error);
        });
    },

    newimganno: (req, res) => {
        let body = req.query.body.replace(' ','%20')
        let data = {
            creator_id: 1,
            body: 'http://thymesis.com/' + req.query.body,
            target: `{type:'Image',format:'image/jpg',id:http://thymesis.com/image%23xywh=${req.query.x},${req.query.y},${req.query.w},${req.query.h}}`
        }
        let ur = 'http://thymesis-api.herokuapp.com/add/annotation/?creator_id=1&body=http://thymesis.com/' + body + '&target={"type":"Image","format":"image/jpg","id":"' + req.query.id + '%23xywh=' + req.query.x + ',' + req.query.y + ',' + req.query.w + ',' + req.query.h + '"}'
        console.log(ur)
        axios.put(ur).then((response) => {
            return res.json(response);
        }).catch((error) => {
            return res.json(error);
        });
    },

    newanno: (req, res) => {
        axios.put(`${annotationUrl}?&target=${req.query.target}&creator_1=1`).then((response) => {
            return res.redirect('/');
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

    getAnnotations: (req, res) => {
        axios.get('https://thymesis-api.herokuapp.com/get/annotation/target/' + req.query.post_id).then((response) => {
            let annotations = Object.values(response.data.message);
            let imageAnnotations = [];
            let textAnnotations = [];
            annotations.forEach((annotation) => {
                if (typeof annotation.target.id !== 'undefined') {
                    if (annotation.target.type === 'Image') {
                        let bodyUrl = annotation.body.split('/'); 
                        let coordinates = annotation.target.id.split('xywh=')[1];
                        let xywh = coordinates.split(',');
                        imageAnnotations.push({
                            body: bodyUrl[bodyUrl.length - 1].replace(/_/g, " "),
                            x: xywh[0],
                            y: xywh[1],
                            w: xywh[2],
                            h: xywh[3],
                        });
                    } 
                }

                if (annotation.target.type === 'Text') {
                    textAnnotations.push({
                        start: annotation.target.selector.start,
                        end: annotation.target.selector.end,
                    });
                }
                
            })
            return res.json({imageAnnotations, textAnnotations});
        });
    },

};

