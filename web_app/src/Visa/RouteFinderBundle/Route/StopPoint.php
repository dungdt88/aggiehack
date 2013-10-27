<?php
/**
 *
 */

namespace Visa\RouteFinderBundle\Route;

/**
 * Class StopPoint
 * @package Visa\RouteFinderBundle\Route
 */
class StopPoint
{
    /**
     * @var float
     */
    protected $longitude;
    /**
     * @var float
     */
    protected $latitude;

    /**
     * @var string
     */
    protected $name;
    
    /**
     * @param float $longitude
     * @param float $latitude
     * @param string $name
     */
    public function __construct($longitude, $latitude, $name = '')
    {
        $this->longitude = $longitude;
        $this->latitude = $latitude;
        $this->name = $name;
    }

    /**
     * @param mixed $latitude
     */
    public function setLatitude($latitude)
    {
        $this->latitude = $latitude;
    }

    /**
     * @return float
     */
    public function getLatitude()
    {
        return $this->latitude;
    }

    /**
     * @param mixed $longitude
     */
    public function setLongitude($longitude)
    {
        $this->longitude = $longitude;
    }

    /**
     * @return float
     */
    public function getLongitude()
    {
        return $this->longitude;
    }

    /**
     * @param string $name
     */
    public function setName($name)
    {
        $this->name = $name;
    }

    /**
     * @return string
     */
    public function getName()
    {
        return $this->name;
    }
    
    
}
