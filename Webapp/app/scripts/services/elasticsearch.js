'use strict';

/**
 * @ngdoc service
 * @name webappApp.ElasticSearch
 * @description
 * # ElasticSearch
 * Service in the webappApp.
 */
angular.module('webappApp')
  .service('ElasticSearch', function (esFactory) {

    return esFactory({
    	host: 'localhost:9200/dataforgood',
  	});
  });
