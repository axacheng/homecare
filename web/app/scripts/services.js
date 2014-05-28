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
    return {
      readTemperature: function(){
        // https://docs.angularjs.org/api/ngResource/service/$resource
        return $resource(homecare_prod_constant.readTemperatureUrl,
                         {},
                         { query: {method:'GET',
                                   params:{user_id:'user_id'},
                                   isArray:true}
        });
      },
      // readmymessage_more: function(){
      //   return $resource(homecare_prod_constant.readmymessageUrl,
      //                    {},
      //                    { query: {method:'GET',
      //                              params:{access_key:'access_key',
      //                                      page:'page'},
      //                              isArray:true}
      //   });
      // },
    };
  }
])

