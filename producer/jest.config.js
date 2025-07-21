module.exports = {
  testEnvironment: 'node',
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  transformIgnorePatterns: [
    'node_modules/(?!(@pact-foundation)/)'
  ],
  moduleFileExtensions: ['js', 'json'],
};
