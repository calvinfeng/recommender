
from incremental_svd_tester import IncrementalSVDTester
from incremental_svd_trainer import IncrementalSVDTrainer

svd_trainer = IncrementalSVDTrainer(
        '../data/100-users/training_movies.csv',
        '../data/100-users/training_ratings.csv',
        '../data/100-users/training_links.csv',
    )
svd_trainer.configure(0.1, 0.15, 8)

print 'Before function optimization:'
print 'Training RMSE: %s' % svd_trainer.training_rmse
print 'CV RMSE: %s' % svd_trainer.cross_validation_rmse

svd_trainer.batch_gradient_descent()

print '\nAfter function optimization:'
print 'Training RMSE: %s' % svd_trainer.training_rmse
print 'CV RMSE: %s' % svd_trainer.cross_validation_rmse

svd_tester = IncrementalSVDTester(
        '../data/10-users/training_ratings.csv',
        svd_trainer.movies
    )
svd_tester.configure(0.1, 0.15, 8)

print 'Before function optimization:'
print 'Training RMSE: %s' % svd_tester.training_rmse
print 'Test RMSE: %s' % svd_tester.test_rmse

print '\nAfter function optimization:'
print 'Training RMSE: %s' % svd_tester.training_rmse
print 'Test RMSE: %s' % svd_tester.test_rmse
