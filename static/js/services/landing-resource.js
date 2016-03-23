(function() {
    'use strict';

    electionChartsApp.factory('landingResource', ['$resource', 'errorHandler', function($resource, errorHandler) {
        var factory = {};

        factory.resource = $resource('/api/landing');

        factory.query = function(id, type){
            var query = this.resource.query(
                { },
                function success(res) {
                    // not implemented
                },
                function error(res) {
                    errorHandler.setError("Error: " + res.error);
                }
            );

            return query;
        };

        factory.get = function(id, type) {
            var get = this.resource.get(
                { },
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
