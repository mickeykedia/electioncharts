(function() {
  'use strict';

  electionChartsApp.factory('partyStateResource', ['$resource', 'errorHandler', function($resource, errorHandler) {

    var factory = {};

    factory.resource = $resource('/api/party/state/:type/:partyId/:stateId');

    factory.query = function(partyId,stateId, type){
      var query = this.resource.query(
        { type: type, partyId: partyId,stateId:stateId },
        function success(res) {
          // not implemented
        },
        function error(res) {
          errorHandler.setError("Error: " + res.error);
        }
      );

      return query;
    };

    factory.get = function(partyId,stateId, type) {
      var get = this.resource.get(
        { type: type, partyId: partyId,stateId:stateId },
        function success(res) {
          // not implemented
        },
        function error(res) {
          errorHandler.setError("Error: " + res.error);
        }
      );

      return get;
    };

    return factory;
  }]);
}());