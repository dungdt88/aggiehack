<?php

namespace Csg\DataBundle\Service;


use Doctrine\DBAL\Connection;

class DistanceCalculator
{
    /**
     * @var GoogleDistanceClient
     */
    protected $googleDistanceClient;
    /**
     * @var \Doctrine\DBAL\Connection
     */
    protected $conn;

    /**
     * @param Connection $conn
     * @param GoogleDistanceClient $googleDistanceClient
     */
    public function __construct(Connection $conn, GoogleDistanceClient $googleDistanceClient)
    {
        $this->conn = $conn;
        $this->googleDistanceClient = $googleDistanceClient;
    }

    /**
     * 
     */
    public function initializeDistances()
    {
        $sql = "
            SELECT id
            FROM location
            ORDER BY id
        ";
        
        $stmt = $this->conn->prepare($sql);
        $stmt->execute();
        
        $locationIds = $stmt->fetchAll(\PDO::FETCH_ASSOC);

        foreach ($locationIds as $startRow) {
            $startLocationId = $startRow['id'];
            
            $insertSql = "
                INSERT IGNORE INTO distance (start_loc_id, end_loc_id)
                VALUES 
            ";
            
            foreach ($locationIds as $endRow) {
                $endLocationId = $endRow['id'];
                
                if ($startLocationId != $endLocationId) {
                    $insertSql .= "({$startLocationId}, {$endLocationId}),";
                }
            }

            $insertSql = trim($insertSql, ', ');
            $this->conn->prepare($insertSql)->execute();
        }
    }
    
    public function calculateDistance($elementsLimit = 2000, $elementsPerRequestLimit = 20)
    {
        $sql = "
            SELECT d.start_loc_id, end_loc_id, 
                l1.latitude AS start_loc_latitude, l1.longitude AS start_loc_longitude,
                l2.latitude AS end_loc_latitude, l2.longitude AS end_loc_longitude
            FROM `distance` d
                JOIN location l1 ON l1.id = d.start_loc_id
                JOIN location l2 ON l2.id = d.end_loc_id
            WHERE distance IS NULL OR time IS NULL
            ORDER BY start_loc_id, end_loc_id
        ";
        
        $stmt = $this->conn->prepare($sql);
        $stmt->execute();
        $rows = array();
        
        while ($row = $stmt->fetch(\PDO::FETCH_ASSOC)) {
            if (!isset($rows[$row['start_loc_id']])) {
                $rows[$row['start_loc_id']] = array(
                    'latitude' => $row['start_loc_latitude'],
                    'longitude' => $row['start_loc_longitude'],
                    'end_loc_ids' => array(),
                );
            }

            if (!isset($rows[$row['end_loc_id']]['end_loc_ids'][$row['start_loc_id']])) {
                $rows[$row['start_loc_id']]['end_loc_ids'][$row['end_loc_id']] = array(
                    'latitude' => $row['end_loc_latitude'],
                    'longitude' => $row['end_loc_longitude'],
                );
            }
        }
        
        $totalElements = 0;
        
        foreach ($rows as $startLocId => $row) {
            if ($elementsPerRequestLimit < sizeof($row['end_loc_ids'])) {
                $endLocIdChunks = array_chunk($row['end_loc_ids'], $elementsPerRequestLimit, true);
                
                foreach ($endLocIdChunks as $endLocIdChunk) {
                    if ($elementsLimit <= $totalElements) {
                        return;
                    }

                    $origins = array(
                        array(
                            $row['latitude'],
                            $row['longitude']
                        )
                    );
                    $destinations = array();
                    
                    foreach ($endLocIdChunk as $endLocId => $endLoc) {
                        $destinations[] = array(
                            $endLoc['latitude'],
                            $endLoc['longitude'],
                        );
                    }
                    
                    $distances = $this->googleDistanceClient->getDistanceMatrix($origins, $destinations);
                    var_dump($distances); die;

                    $totalElements += sizeof($destinations);
                }
            }
        }
    }
}