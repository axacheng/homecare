/*
 * angular-phonegap-push-notification v0.0.3
 * (c) 2014 Patrick Heneise, patrickheneise.com
 * License: MIT
 */

'use strict';

angular.module('cordova', [])

  .factory('cordovaReady', function ($rootScope, $q) {
    var loadingDeferred = $q.defer();

    document.addEventListener('deviceready', function () {
      $rootScope.$apply(loadingDeferred.resolve);
    });
    
    return function cordovaReady() {
      console.log('cordovaReady')
      return loadingDeferred.promise;
    };
  })

  .service('phone', function () {
    this.isAndroid = function () {
      var uagent = navigator.userAgent.toLowerCase();
      return uagent.search('android') > -1 ? true : false;
    };
  })

  .factory('push', function ($rootScope, phone, cordovaReady) {
    return {
      registerPush: function (fn) {
        cordovaReady().then(function () {
          console.log('ok')
          var
            pushNotification = window.plugins.pushNotification,
            successHandler = function (result) {
              console.log('rrrrrrrrrrrrrrrrr:', result)
            },
            errorHandler = function (error) {
              console.log('eeeeeee:', error)
            },
            tokenHandler = function (result) {
              return fn({
                'type': 'registration',
                'id': result,
                'device': 'ios'
              });
            };

          // onNotificationGCM = function (event) {
          //   switch (event.event) {
          //     case 'registered':
          //       if (event.regid.length > 0) {
          //         return fn({
          //           'type': 'registration',
          //           'id': event.regid,
          //           'device': 'android'
          //         });
          //       }
          //       break;

          //     case 'message':
          //       if (event.foreground) {
          //         var my_media = new Media("/android_asset/www/" + event.soundname);
          //         my_media.play();
          //       } else {
          //         if (event.coldstart) {
          //         } else {
          //         }
          //       }
          //       break;

          //     case 'error':
          //       break;

          //     default:
          //       break;
          //   }
          // };


          if (phone.isAndroid()) {
            console.log('register android');

            pushNotification.register(successHandler, errorHandler, {
              'senderID': '1060962448908',
              'ecb': 'onNotificationGCM'
            });
          } else {
            console.log('register ios');
            pushNotification.register(tokenHandler, errorHandler, {
              'badge': 'true',
              'sound': 'true',
              'alert': 'true',
              'ecb': 'onNotificationAPN'
            });
          }
        });
      }
    };
  });

// function onNotificationAPN(event) {
//   if (event.alert) {
//     navigator.notification.alert(event.alert);
//   }

//   if (event.sound) {
//     var snd = new Media(event.sound);
//     snd.play();
//   }

//   if (event.badge) {
//     pushNotification.setApplicationIconBadgeNumber(successHandler, errorHandler, event.badge);
//   }
// }

function onNotificationGCM(event) {
  //console.log(event)
  console.log('onNotificationGCMMMMMMMMMMMMMMMMMMMmmmm')
  switch (event.event) {
    case 'registered':
      console.log('registereddddddddddd')
      if (event.regid.length > 0) {
        localStorage.setItem('device_id', event.regid);
        localStorage.setItem('device', 'android');
      }
      break;

    case 'message':
      console.log('mmmmmmmmmmmm')
      if (event.foreground) {
        var my_media = new Media("/android_asset/www/" + event.soundname);
        my_media.play();
      } else {
        if (event.coldstart) {
        } else {
        }
      }
      break;

    case 'error':
      console.log('error');
      break;

    default:
      console.log('default');
      break;
  }
}
