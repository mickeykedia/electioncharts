(function(){
  'use strict';

  electionChartsApp.controller('StateListCtrl', ['$scope', 'stateResource', function ($scope, stateResource) {

    $scope.stateList = stateResource.query();

  }]);
}());
