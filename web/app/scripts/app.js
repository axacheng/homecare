// Ionic Starter App

// angular.module is a global place for creating, registering and retrieving Angular modules
// 'starter' is the name of this angular module example (also set in a <body> attribute in index.html)
// the 2nd parameter is an array of 'requires'
// 'starter.services' is found in services.js
// 'starter.controllers' is found in controllers.js
'use strict';


angular.module('homecareConstant', [])
.constant('homecare_prod_constant', {
  //accessKey:'axatest',
  //gcmAppID:'1060962448908',
  queryTemperatureUrl:'http://192.168.0.106:8080/_ah/api/homecare/v1/queryTemperature',
});


angular.module('Web', ['ionic', 'Web.services', 'Web.controllers'])
.run(function($ionicPlatform) {
  $ionicPlatform.ready(function() {
    if(window.StatusBar) {
      StatusBar.styleDefault();
    }
  });
})

.config(function($stateProvider, $urlRouterProvider) {
  // Ionic uses AngularUI Router which uses the concept of states
  // Learn more here: https://github.com/angular-ui/ui-router
  // Set up the various states which the app can be in.
  // Each state's controller can be found in controllers.js
  $stateProvider
    // the pet tab has its own child nav-view and history
    .state('main', {
      url: '/main',
      abstract: true,
      templateUrl: 'templates/main.html',
    })
    .state('main.list', {
      url: '/list',  // /main/shell
      views: {
        'mainContent': {
          templateUrl: 'templates/main-list.html',
          controller: ''
        }
      }
    })
    .state('main.remote', {
      url: '/remote', // /main/remote
      views: {
        'mainContent': {
          templateUrl: 'templates/remote-index.html',
          controller: ''
        }
      }
    })
    .state('main.temperature', {
      url: '/temperature', // /main/remote/temperature
      views: {
        'mainContent': {
          templateUrl: 'templates/temperature.html',
          controller: 'TemperatureCtrl'
        }
      }
    });
  // if none of the above states are matched, use this as the fallback
  $urlRouterProvider.otherwise('/main/list');

});

