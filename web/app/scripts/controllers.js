'use strict';
angular.module('Web.controllers', [])


// A simple controller that fetches a list of data from a service
.controller('PetIndexCtrl', function($scope, PetService) {
  // "Pets" is a service returning mock data (services.js)
  $scope.pets = PetService.all();
})


// A simple controller that shows a tapped item's data
.controller('PetDetailCtrl', function($scope, $stateParams, PetService) {
  // "Pets" is a service returning mock data (services.js)
  $scope.pet = PetService.get($stateParams.petId);
})

// A simple controller that shows a tapped item's data
.controller('TemperatureCtrl',['$scope', '$stateParams', 'TemperatureService', function($scope, $stateParams, TemperatureService) {
  // "Pets" is a service returning mock data (services.js)
  //$scope.temperature = TemperatureService.readTemperature();
  $scope.temperature = 99;
}]);
