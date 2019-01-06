/**
 * Route Mappings
 * (sails.config.routes)
 *
 * Your routes tell Sails what to do each time it receives a request.
 *
 * For more information on configuring custom routes, check out:
 * https://sailsjs.com/anatomy/config/routes-js
 */

module.exports.routes = {

  /***************************************************************************
  *                                                                          *
  * Make the view located at `views/homepage.ejs` your home page.            *
  *                                                                          *
  * (Alternatively, remove this and add an `index.html` file in your         *
  * `assets` directory)                                                      *
  *                                                                          *
  ***************************************************************************/

  // Home route
  '/': 'HomeController.index',

  // Login routes
  '/login': 'UserController.login',
  '/logout': 'UserController.logout',
  '/register': 'UserController.signup',

  // User routes
  '/userpage/:user': 'UserController.page',

  // Memory routes
  '/create': 'PostController.create',
  '/memory/:id': 'PostController.page',
  '/annotate/:id': 'PostController.annotate',
  '/annotateimg/:id': 'PostController.annotateimg',
  '/annotate/new': 'PostController.newanno',

  // Search
  '/search': 'PostController.search',

  /***************************************************************************
  *                                                                          *
  * More custom routes here...                                               *
  * (See https://sailsjs.com/config/routes for examples.)                    *
  *                                                                          *
  * If a request to a URL doesn't match any of the routes in this file, it   *
  * is matched against "shadow routes" (e.g. blueprint routes).  If it does  *
  * not match any of those, it is matched against static assets.             *
  *                                                                          *
  ***************************************************************************/


};
