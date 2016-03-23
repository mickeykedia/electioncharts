(function(){
  'use strict';

  electionChartsApp.controller('CandidateCtrl', ['$scope', '$routeParams', '$interval', 'candidateResource', function ($scope, $routeParams, $interval, candidateResource) {
    var candidateId = $routeParams.candidateId;
    $scope.candidate = candidateResource.get(candidateId);
    var results = candidateResource.query(candidateId, 'result');
    $scope.results2009 = candidateResource.query(candidateId, 'result2009');

    var interval_promise;
    if (!angular.isDefined(interval_promise)) {
      $interval(function(){
        results = candidateResource.query(candidateId, 'result');
      }, 60*1000);
    }
    
    $scope.$on('$destroy', function() {
      if (angular.isDefined(interval_promise)) {
        $interval.cancel(interval_promise);
        interval_promise = undefined;
      }
    });

    $scope.results = results;

  }]);
}());
