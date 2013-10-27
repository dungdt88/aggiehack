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
    
    public function getSegmentCount()
    {
        return sizeof($this->segments);
    }
}
