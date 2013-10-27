<?php
namespace Visa\RouteFinderBundle\Service;


/**
 * Class RouteFinder
 * @package Visa\RouteFinderBundle\Service
 */
use Visa\RouteFinderBundle\Route\FinderClient;
use Visa\RouteFinderBundle\Route\StopPoint;

/**
 * Class RouteFinder
 * @package Visa\RouteFinderBundle\Service
 */
class RouteFinder
{
    /**
     * @var \Visa\RouteFinderBundle\Route\FinderClient
     */
    protected $finderClient;
    
    /**
     * @param FinderClient $finderClient
     */
    public function __construct(FinderClient $finderClient)
    {
        $this->finderClient = $finderClient;
    }

    /**
     * @param $fromLatitude
     * @param $fromLongitude
     * @param $toLatitude
     * @param $toLongitude
     * @param $startTime
     * @param null $sorting
     * @return array
     */
    public function findRoutes($fromLatitude, $fromLongitude, $toLatitude, $toLongitude, $startTime, $sorting = null)
    {
        $from = new StopPoint($fromLongitude, $fromLatitude);
        $to = new StopPoint($toLongitude, $toLatitude);
        $startingTime = new \DateTime(date('H:i:s', strtotime($startTime)));
        
        if ($routes = $this->finderClient->findRoutes($from, $to, $startingTime)) {
            if ($sorting) {
                $routes = $this->sortRoutes($routes, $sorting);
            }
            
            return $routes;
        }
        
        
        return array();
    }

    /**
     * @param $result
     * @return array
     */
    protected function formatResult($result)
    {
        $result = trim($result);
        $rows = explode("\n", $result);
        $routes = array();
        
        foreach ($rows as $row) {
            $p = explode(",", $row);
            $routes[] = array(
                'from' => $p[0],
                'to' => $p[1],
                'time' => $p[2],
                'type' => $p[3]
            );
            
        }
        return $routes;
    }

    /**
     * 
     * @param array $routes
     * @param string $sorting
     * @return array
     */
    protected function sortRoutes(array $routes, $sorting)
    {
        return $routes;
    }
}