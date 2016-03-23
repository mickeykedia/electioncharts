(function(){
  'use strict';

  electionChartsApp.controller('PartyCtrl', ['$scope', '$routeParams', '$interval', 'partyResource', function ($scope, $routeParams, $interval, partyResource) {
    var partyId = $routeParams.partyId;
    $scope.party = partyResource.get(partyId);
    $scope.results = partyResource.get(partyId, 'result');
    var detailed_results_undeclared = partyResource.query(partyId, 'detailed_result_undeclared');
    var detailed_results_declared = partyResource.query(partyId, 'detailed_result_declared');
    var detailed_results = {"declared":[],"undeclared":[]};
    var statewise_results = partyResource.query(partyId, 'statewise_result');

    var interval_promise;
    if (!angular.isDefined(interval_promise)) {
      $interval(function(){
        detailed_results_undeclared = partyResource.query(partyId, 'detailed_result_undeclared');
        detailed_results_declared = partyResource.query(partyId, 'detailed_result_declared');
        statewise_results = partyResource.query(partyId, 'statewise_result');
      }, 60*1000);
    }
    
    $scope.$on('$destroy', function() {
      if (angular.isDefined(interval_promise)) {
        $interval.cancel(interval_promise);
        interval_promise = undefined;
      }
    });

    $scope.statewise_results = statewise_results;
    $scope.show = "all";
    $scope.isCollapsed = false;
    var one_done = false;

    detailed_results_declared.$promise.then(function(detailed_results_declared){
        detailed_results.declared = detailed_results_declared;
        $scope.detailed_results_declared = detailed_results_declared;
        if(one_done){
            $scope.detailed_results = detailed_results;
        }
        one_done= true;

    });

    detailed_results_undeclared.$promise.then(function(detailed_results_undeclared){
        detailed_results.undeclared = detailed_results_undeclared;
        $scope.detailed_results_undeclared = detailed_results_undeclared;

        if(one_done){
            $scope.detailed_results = detailed_results;
        }
        one_done=true;
    });
  }]);
}());
