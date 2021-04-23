from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DataQualityOperator(BaseOperator):

    ui_color = '#89DA59'

    @apply_defaults
    def __init__(self,
                 default_checks=[],
                 redshift_conn_id="",
                 *args, **kwargs):

        super(DataQualityOperator, self).__init__(*args, **kwargs)
        self.default_checks = default_checks
        self.redshift_conn_id = redshift_conn_id

    def execute(self, context):
        if len(self.default_checks) <= 0:
            self.log.info("No data quality check provided")
            return
        
        redshift_hook = PostgresHook(self.redshift_conn_id)
        error_count = 0
        failed_tests = []
        
        for check in self.default_checks:
            sql = check.get('check_sql')
            result_check = check.get('result_check')
            
            try:
                records = redshift_hook.get_records(sql)[0]
            except Exception as e:
                self.log.info(f"Query failed with exception: {e}")
                
            if result_check != records[0]:
                error_count += 1
                failed_tests.append(sql)
                
            if error_count > 0:
                self.log.info('Tests Failed')
                self.log.info(failed_tests)
                raise ValueError('Data quality check failed')
            else:
                self.log.info("All data quality checks passed")
                
        
        
        self.log.info('DataQualityOperator not implemented yet')
        
        
