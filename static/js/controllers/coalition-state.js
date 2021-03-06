(function(){
    'use strict';

    electionChartsApp.controller('CoalitionStateCtrl', ['$scope', '$routeParams', 'coalitionStateResource','coalitionResource','stateResource', function ($scope, $routeParams, coalitionStateResource,coalitionResource,stateResource) {
        var coalitionId = $routeParams.coalitionId;
        var stateId = $routeParams.stateId;

        $scope.coalition = coalitionResource.get(coalitionId);
        $scope.state = stateResource.get(stateId);
        var parties = coalitionStateResource.query(coalitionId, stateId,'result');
        var detailed_results_undeclared = coalitionStateResource.query(coalitionId, stateId,'detailed_result_undeclared');
        var detailed_results_declared = coalitionStateResource.query(coalitionId,stateId, 'detailed_result_declared');
        var detailed_results = {"declared":[],"undeclared":[]};

        var results = {};
        $scope.show = "all";
        var one_done = false;

        detailed_results_declared.$promise.then(function(detailed_results_declared){
            detailed_results.declared = detailed_results_declared;
            $scope.detailed_results_declared = detailed_results_declared;
            if(one_done){
                $scope.detailed_results = detailed_results;
            }
            one_done=true;
        });

        detailed_results_undeclared.$promise.then(function(detailed_results_undeclared){
            detailed_results.undeclared = detailed_results_undeclared;
            $scope.detailed_results_undeclared = detailed_results_undeclared;
            if(one_done){
                $scope.detailed_results = detailed_results;
            }
            one_done=true;
        });
        parties.$promise.then(function(parties){

            results.wins = 0;
            results.leads = 0;
            results.swing = 0;
            results.vote_percentage=0
            results.update_time="";
            for(var p in parties){
                if(parties[p].wins){
                    results.wins = results.wins+ parties[p].wins;
                }
                if(parties[p].leads){
                    results.leads = results.leads+ parties[p].leads;
                }
                if(parties[p].swing){
                    results.swing = results.swing+ parties[p].swing;
                }
                if(parties[p].vote_percentage){
                    results.vote_percentage = results.vote_percentage +parseFloat(parties[p].vote_percentage);
                }
                if(parties[p].update_time){
                    results.update_time = parties[p].update_time;
                }
//                results.vote_percentage = results.vote_percentage+ p.vote_percentage;
            }
            results.vote_percentage = Number(results.vote_percentage.toFixed(2));
        });

        $scope.results = results;
        $scope.parties = parties;
    }]);
}());
