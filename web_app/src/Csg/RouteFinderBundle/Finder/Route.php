<?php

namespace Csg\RouteFinderBundle\Finder;


class Route implements \Iterator
{
    /**
     * @var array
     */
    protected $segments = array();

    /**
     * 
     */
    public function __construct()
    {

    }
    
    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Move forward to next element
     * @link http://php.net/manual/en/iterator.next.php
     * @return void Any returned value is ignored.
     */
    public function next()
    {
        next($this->segments);
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Return the key of the current element
     * @link http://php.net/manual/en/iterator.key.php
     * @return mixed scalar on success, or null on failure.
     */
    public function key()
    {
        return key($this->segments);
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Checks if current position is valid
     * @link http://php.net/manual/en/iterator.valid.php
     * @return boolean The return value will be casted to boolean and then evaluated.
     * Returns true on success or false on failure.
     */
    public function valid()
    {
        $key = key($this->segments);
        
        return ($key !== null && $key !== false);
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Rewind the Iterator to the first element
     * @link http://php.net/manual/en/iterator.rewind.php
     * @return void Any returned value is ignored.
     */
    public function rewind()
    {
        reset($this->segments);
    }

    /**
     * (PHP 5 &gt;= 5.0.0)<br/>
     * Return the current element
     * @link http://php.net/manual/en/iterator.current.php
     * @return mixed Can return any type.
     */
    public function current()
    {
        return current($this->segments);
    }


    /**
     * @param Segment $segment
     * @return $this
     */
    public function addSegment(Segment $segment)
    {
        $this->segments[] = $segment;
        
        return $this;
    }

    /**
     * @return array
     */
    public function getSegments()
    {
        return $this->segments;
    }

    /**
     * @param $index
     * @return Segment|null
     */
    public function getSegment($index)
    {
        return isset($this->segments[$index]) ? $this->segments[$index] : null;
    }

    /**
     * @return float
     */
    public function getDuration()
    {
        $duration = 0.0;

        /** @var $segment Segment */
        foreach ($this->segments as $segment) {
            $duration += $segment->getDuration();
        }
        
        return $duration;
    }

    /**
     * @return string
     */
    public function getNiceDuration()
    {
        $duration = $this->getDuration();
        $niceDuration = '';
        $mapping = array(
            86400 => 'd',
            3600 => 'h',
            60 => 'm',
        );
        
        foreach ($mapping as $threshold => $text) {
            if ($duration >= $threshold) {
                $niceDuration .= (int) ($duration / $threshold) . "$text ";
                $duration = $duration % $threshold;
            }
        }
        
        if ($duration > 0) {
            $niceDuration .= $duration . 's';
        }
        
        return $niceDuration;
    }

    /**
     * @return string
     */
    public function getJsonBusStops()
    {
        $allStops = array();
        
        foreach ($this->segments as $segment) {
            /** @var $segment Segment */
            foreach (array($segment->getStart(), $segment->getEnd()) as $stop) {
                /** @var $stop StopPoint */
                $isExisting = false;
                foreach ($allStops as $_stop) {
                    if ($stop->equals($_stop)) {
                        $isExisting = true;
                        break;
                    }
                }
                
                if (!$isExisting) {
                    $allStops[] = $stop;
                }
            }
        }
        
        $allStopsArray = array();
        
        foreach ($allStops as $stop) {
            $allStopsArray[] = array(
                'name' => $stop->getName(),
                'latitude' => $stop->getLatitude(),
                'longitude' => $stop->getLongitude(),
            );
        }
        
        return json_encode($allStopsArray);
    }

    /**
     * @return int
     */
    public function getSegmentCount()
    {
        return sizeof($this->segments);
    }


    /**
     * @return \DateTime
     */
    public function getArrivalTime()
    {
        if (sizeof($this->segments)) {
            /** @var $lastSegment Segment */
            $lastSegment = null;
            
            foreach ($this->segments as $segment) {
                $lastSegment = $segment;
            }
            
            return new \DateTime('@' . ($lastSegment->getTime()->getTimestamp() + $lastSegment->getDuration())); 
        }
        
        return null;
    }
}
