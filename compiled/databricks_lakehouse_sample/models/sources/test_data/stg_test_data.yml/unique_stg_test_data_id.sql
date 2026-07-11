
    
    

select
    id as unique_field,
    count(*) as n_records

from `workspace`.`project_prod`.`stg_test_data`
where id is not null
group by id
having count(*) > 1


