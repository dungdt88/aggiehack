<?php
namespace Csg\RouteFinderBundle\Service;


/**
 * Class RouteFinder
 * @package Csg\RouteFinderBundle\Service
 */
use Csg\RouteFinderBundle\Finder\FinderClient;
use Csg\RouteFinderBundle\Finder\StopPoint;

/**
 * Class RouteFinder
 * @package Csg\RouteFinderBundle\Service
 */
class RouteFinder
{
    /**
     * @var \Csg\RouteFinderBundle\Finder\FinderClient
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
     * 
     * @param float $fromLatitude
     * @param float $fromLongitude
     * @param float $toLatitude
     * @param float $toLongitude
     * @param string $startTime
     * @param string $sorting
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