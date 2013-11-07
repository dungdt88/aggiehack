<?php

namespace Csg\DataBundle\Service;


/**
 * Class LocationImporter
 * @package Csg\DataBundle\Service
 */
class LocationImporter extends AbstractImporter
{
    /**
     * @var \PDOStatement
     */
    protected $queryStmt;

    /**
     * 
     */
    protected function preProcess()
    {
        $sql = "
            INSERT IGNORE INTO `location` (`uid`, `code`, `name`, `latitude`, `longitude`)
            VALUES (:uid, :code, :name, :latitude, :longitude)
        ";

        $this->queryStmt = $this->conn->prepare($sql);
    }
    
    /**
     * @param array $values
     * @return mixed
     */
    protected function processRow(array $values)
    {
        $this->queryStmt->bindValue('uid', $this->getValue($values, 'stop_id'));
        $this->queryStmt->bindValue('code', $this->getValue($values, 'stop_code'));
        $this->queryStmt->bindValue('name', $this->getValue($values, 'stop_name'));
        $this->queryStmt->bindValue('latitude', $this->getValue($values, 'stop_lat'));
        $this->queryStmt->bindValue('longitude', $this->getValue($values, 'stop_lon'));
        
        $this->queryStmt->execute();
    }
}
