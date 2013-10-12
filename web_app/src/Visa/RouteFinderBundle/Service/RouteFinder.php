<?php
namespace Visa\RouteFinderBundle\Service;


/**
 * Class RouteFinder
 * @package Visa\RouteFinderBundle\Service
 */
class RouteFinder
{
    /**
     *
     */
    public function __construct()
    {
        
    }

    /**
     * @param $fromLatitude
     * @param $fromLongitude
     * @param $toLatitude
     * @param $toLongitude
     * @param $startTime
     * @return array
     */
    public function findRoutes($fromLatitude, $fromLongitude, $toLatitude, $toLongitude, $startTime)
    {
        return array();
    }
}