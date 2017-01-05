var buildApp = angular.module('buildApp', ['ngRoute']);

buildApp.config(function($routeProvider){
	$routeProvider
		.when('/',
		{
			controller: 'BuildController',
			templateUrl: 'templates/list.html'
		})
		.otherwise({redirectTo: '/'});
	})
	.controller('BuildController', function($scope, $interval, buildFactory) {

		$scope.statusVisible = false;

		$scope.getGlyphClass = function(tile) {
			if(tile.state == 'RUNNING') {
				return 'glyphicon glyphicon-refresh glyphicon-refresh-animate';
			}
			else if(tile.paused) {
				return 'glyphicon glyphicon-pause';
			}
			else if(tile.status == 'PASSED' || tile.status == 'ALL OK') {
				return 'glyphicon glyphicon-ok';
			}
			else if(tile.status == 'FAILED') {
				return 'glyphicon glyphicon-exclamation-sign';
			}
			return 'glyphicon glyphicon-question-sign';
		}

		$scope.getPanelClass = function(tile){
			if(tile.state == 'RUNNING') {
				return 'alert alert-dismissible alert-success';
			}
			else if(tile.paused == true) {
				return 'alert alert-dismissible alert-info';
			}
			else if(tile.status == 'PASSED' || tile.status == 'ALL OK') {
				return 'alert alert-dismissible alert-success';
			}
			else if(tile.status == 'CANCELLED') {
				return 'alert alert-dismissible alert-info';
			}
			else if(tile.status == 'FAILED') {
				return 'alert alert-dismissible alert-danger';
			}

			return 'alert alert-dismissible alert-warning';
		}

		$scope.reload = function() {
			$scope.statusVisible = true;

			buildFactory.getBuilds()
				.then(function(response) {
					$scope.buildData = response.data
				})
				.then(function() {
					$scope.builds = $scope.buildData.map(function(b) { return buildFactory.decodeBuild(b, []); });
				})
				.then(function() {
					$scope.tiles = buildFactory.generateTiles($scope.builds)
				})
				.then(function() {
					$scope.statusVisible = false;
				});
		    };

			$scope.reload();

			$interval(function () {$scope.reload()}, 10000);
	});