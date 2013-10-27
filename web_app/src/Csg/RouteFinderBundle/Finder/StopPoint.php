<?php
/**
 *
 */

namespace Csg\RouteFinderBundle\Finder;

/**
 * Class StopPoint
 * @package Csg\RouteFinderBundle\Finder
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
     * @return $this
     */
    public function setLatitude($latitude)
    {
        $this->latitude = $latitude;

        return $this;
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
     * @return $this
     */
    public function setLongitude($longitude)
    {
        $this->longitude = $longitude;
        
        return $this;
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
     * @return $this
     */
    public function setName($name)
    {
        $this->name = $name;
        
        return $this;
    }

    /**
     * @return string
     */
    public function getName()
    {
        return $this->name;
    }
    
    
}
