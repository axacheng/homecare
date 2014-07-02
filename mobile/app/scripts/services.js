'use strict';
angular.module('Web.services', ['homecareConstant', 'ngResource'])

/**
 * A simple example service that returns some data.
 */
.factory('PetService', function() {
  // Might use a resource here that returns a JSON array

  // Some fake testing data
  var pets = [
    { id: 0, title: 'Cats', description: 'Furry little creatures. Obsessed with plotting assassination, but never following through on it.' },
    { id: 1, title: 'Dogs', description: 'Lovable. Loyal almost to a fault. Smarter than they let on.' },
    { id: 2, title: 'Turtles', description: 'Everyone likes turtles.' },
    { id: 3, title: 'Sharks', description: 'An advanced pet. Needs millions of gallons of salt water. Will happily eat you.' }
  ];

  return {
    all: function() {
      return pets;
    },
    get: function(petId) {
      // Simple index lookup
      return pets[petId];
    }
  };
})

.factory('TemperatureService', ['homecare_prod_constant', '$resource',
  function(homecare_prod_constant, $resource) {
    var temperatureObject = []
    return {
      queryTemperature: function(userId){
        /*
          TemperatureService.queryTemperature()
    .get({user_id:$stateParams.userId})
      .$promise.then(function(endpoint_return){
        $scope.temperature = endpoint_return.items[0].current_temperature;
        $scope.current_time = endpoint_return.items[0].ctime;
  });
*/

        var Temperature = $resource(homecare_prod_constant.queryTemperatureUrl);
        return Temperature.get({user_id:userId}).$promise;
        //return Temperature.get({user_id:userId}).$promise.then();
        //return Temperature.get({user_id:userId}).$promise
            //console.log(endpoint_return);
            //return endpoint_return;
            //return 99;
      }
    };
  }
]);