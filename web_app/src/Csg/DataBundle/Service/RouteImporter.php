<?php

namespace Csg\DataBundle\Service;


class RouteImporter extends AbstractImporter
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
            INSERT IGNORE INTO `route` (`uid`, `name`, `short_name`, `description`)
            VALUES (:uid, :name, :short_name, :description)
        ";

        $this->queryStmt = $this->conn->prepare($sql);
    }
    
    /**
     * @param array $values
     * @return mixed
     */
    protected function processRow(array $values)
    {
        $this->queryStmt->bindValue('uid', $this->getValue($values, 'route_id'));
        $this->queryStmt->bindValue('name', $this->getValue($values, 'route_long_name'));
        $this->queryStmt->bindValue('short_name', $this->getValue($values, 'route_short_name'));
        $this->queryStmt->bindValue('description', $this->getValue($values, 'route_desc'));

        $this->queryStmt->execute();
    }
}
