(function(){
  'use strict';

  electionChartsApp.controller('PartyStateCtrl', ['$scope', '$routeParams', 'partyStateResource','partyResource','stateResource', function ($scope, $routeParams,partyStateResource, partyResource,stateResource) {

    var partyId = $routeParams.partyId;
      var stateId = $routeParams.stateId;
    $scope.party = partyResource.get(partyId);
      $scope.state = stateResource.get(stateId);
    $scope.results = partyStateResource.get(partyId,stateId, 'result');
      $scope.show = "all";
    var detailed_results_undeclared = partyStateResource.query(partyId,stateId, 'detailed_result_undeclared');
      var detailed_results_declared = partyStateResource.query(partyId,stateId, 'detailed_result_declared');
      var detailed_results = {"declared":[],"undeclared":[]};

      var one_done = false;
      detailed_results_declared.$promise.then(function(detailed_results_declared){
          detailed_results.declared = detailed_results_declared;
          $scope.detailed_results_declared = detailed_results_declared;
          if(one_done){
              $scope.detailed_results = detailed_results;
          }
          one_done=true;
      })

      detailed_results_undeclared.$promise.then(function(detailed_results_undeclared){
          detailed_results.undeclared = detailed_results_undeclared;
          $scope.detailed_results_undeclared = detailed_results_undeclared;
          if(one_done){
              $scope.detailed_results = detailed_results;
          }
          one_done=true;
      })
  }]);
}());