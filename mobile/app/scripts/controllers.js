'use strict';
angular.module('Web.controllers', ['cordova'])
//Main list controller, includes GCM registration.
.controller('MainListCtrl', ['$scope', 'push', function($scope, push) {
  // run registerPush() method from push.js file, it will use localStorage.setItem
  // To save device GCM id as key 'device_id' 
  push.registerPush();

  // Get this phone GCM id from localStorage
  $scope.deviceId = localStorage.getItem('device_id');


}])

// Get temperature
.controller('TemperatureCtrl',['$scope', '$stateParams', 'TemperatureService', function($scope, $stateParams, TemperatureService) {
  //TemperatureService.queryTemperature($stateParams.userId).then(function(endpoint_return){
  TemperatureService.queryTemperature('axa').then(function(endpoint_return){
    console.log(endpoint_return.items[0])

    if (endpoint_return.status === 'ok' && endpoint_return.items) {
      $scope.current_temperature = endpoint_return.items[0].current_temperature;
      $scope.current_time = endpoint_return.items[0].ctime;      
    }
    else {
      $scope.current_time = Date.now()
    }
  });
}]);
