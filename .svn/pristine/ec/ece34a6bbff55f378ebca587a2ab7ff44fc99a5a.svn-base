(function() {
    'use strict';

    electionChartsApp.factory('coalitionResource', ['$resource', 'errorHandler', function($resource, errorHandler) {
        var factory = {};

        factory.resource = $resource('/api/coalition/:type/:id');

        factory.query = function(id, type){
            var query = this.resource.query(
                { type: type, id: id },
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
                { type: type, id:id },
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
