const assert = require('assert');
const request = require('supertest');
const { app, collectVotesFromResult } = require('../server');

describe('Result Microservice Unit Tests', function () {
  describe('collectVotesFromResult', function () {
    it('should aggregate votes correctly from DB rows', function () {
      const mockResult = {
        rows: [
          { vote: 'a', count: '12' },
          { vote: 'b', count: '8' }
        ]
      };
      const votes = collectVotesFromResult(mockResult);
      assert.strictEqual(votes.a, 12);
      assert.strictEqual(votes.b, 8);
    });

    it('should handle single option votes correctly', function () {
      const mockResult = {
        rows: [
          { vote: 'a', count: '5' }
        ]
      };
      const votes = collectVotesFromResult(mockResult);
      assert.strictEqual(votes.a, 5);
      assert.strictEqual(votes.b, 0);
    });

    it('should handle empty DB rows', function () {
      const mockResult = { rows: [] };
      const votes = collectVotesFromResult(mockResult);
      assert.strictEqual(votes.a, 0);
      assert.strictEqual(votes.b, 0);
    });
  });

  describe('GET /', function () {
    it('should serve index.html with 200 OK', function (done) {
      request(app)
        .get('/')
        .expect('Content-Type', /html/)
        .expect(200, done);
    });
  });
});
