(function(){
  'use strict';

  electionChartsApp.controller('CandidateListCtrl', ['$scope', 'candidateResource', function ($scope, candidateResource) {

    $scope.candidateList = candidateResource.query();

  }]);
}());
