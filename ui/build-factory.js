angular.module('buildApp').factory('buildFactory', function($http) {
	var factory = {};

	factory.getBuilds = function() {
		return $http.get('/wsgi/build-status');
	};

	factory.decodeBuild = function(build, runningBuilds) {
	    // Can't find a better way to see if the build is currently running :(
		var state = build.status.toUpperCase() == 'UNKNOWN' ? 'RUNNING' : 'FINISHED';

		return {
				'id': build.pipeline,
				'name': build.pipeline,
				'paused': build.paused,
				'status': build.status.toUpperCase(),
				'state': state,
				'group': build.group,
		}
	};

	factory.generateTiles = function(builds) {
		var grouped = groupBy(builds, function(x) { return x.group });
		var tiles = [];
		grouped.forEach(function(group) {
			var badChildren = group.filter(function(b) { return b.status == 'FAILED' });
			var goodChildren = group.filter(function(b) { return b.status != 'FAILED' });

			badChildren.forEach(function(b) { tiles.push(b) });

			if(goodChildren.length > 1) {
				var groupState = goodChildren[0].state;
				goodChildren.filter(function(b) { return b.state == 'RUNNING' }).forEach(function(x) { groupState = x.state });

				var tile = {
                        'name': goodChildren[0].group,
                        'group': goodChildren[0].group,
                        'buildCount': goodChildren.length,
                        'status': 'ALL OK',
                        'state': groupState
				    };
				tiles.push(tile);
			}
			else {
				goodChildren.forEach(function(b) { tiles.push(b) });
			}
		});

		return tiles
	};

	return factory;
});