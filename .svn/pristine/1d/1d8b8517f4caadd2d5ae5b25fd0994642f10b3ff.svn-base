(function() {
    'use strict';

    electionChartsApp.factory('coalitionStateResource', ['$resource', 'errorHandler', function($resource, errorHandler) {

        var factory = {};

        factory.resource = $resource('/api/coalition/state/:type/:coalitionId/:stateId');


        factory.query = function(coalitionId,stateId, type){
            var query = this.resource.query(
                { type: type, coalitionId: coalitionId,stateId:stateId },
                function success(res) {
                    // not implemented
                },
                function error(res) {
                    errorHandler.setError("Error: " + res.error);
                }
            );

            return query;
        };

        factory.get = function(coalitionId,stateId, type) {
            var get = this.resource.get(
                { type: type, coalitionId: coalitionId,stateId:stateId },
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
