<?php

namespace Csg\DataBundle\Service;

use Doctrine\DBAL\Connection;
use Symfony\Component\HttpFoundation\File\Exception\FileNotFoundException;

/**
 * Class AbstractImporter
 * @package Csg\DataBundle\Service
 */
abstract class AbstractImporter
{
    /**
     * @var \Doctrine\DBAL\Connection
     */
    protected $conn;
    
    /**
     * @var string
     */
    protected $source;

    /**
     * @var array
     */
    protected $header2Index;

    /**
     * @param Connection $conn
     */
    public function __construct(Connection $conn)
    {
        $this->conn = $conn;
        $this->header2Index = array();
    }

    /**
     * @param mixed $source
     * @throws \Symfony\Component\HttpFoundation\File\Exception\FileNotFoundException
     * @return $this
     */
    public function setSource($source)
    {
        if (!file_exists($source)) {
            throw new FileNotFoundException($source);
        }

        $this->source = $source;

        return $this;
    }

    /**
     * @return mixed
     */
    public function getSource()
    {
        return $this->source;
    }

    /**
     * 
     */
    public function process()
    {
        if ($this->source && $handle = fopen($this->source, 'r')) {
            $this->preProcess();
            $isHeader = true;

            while ($row = fgets($handle)) {
                if ($isHeader) {
                    $headers = explode(',', $row);
                    
                    foreach ($headers as $index => $header) {
                        $this->header2Index[$header] = $index;
                    }
                    
                    $isHeader = false;
                    continue;
                }
                
                $values = explode(',', $row);
                $this->processRow($values);
            }

            $this->postProcess();
        }
    }

    /**
     * @param array $values
     * @return mixed
     */
    abstract protected function processRow(array $values);

    /**
     * 
     */
    protected function preProcess()
    {
        
    }

    /**
     * 
     */
    protected function postProcess()
    {
        
    }

    /**
     * @param array $values
     * @param string $header
     * @return null
     */
    protected function getValue(array $values, $header)
    {
        if (isset($this->header2Index[$header]) && isset($values[$this->header2Index[$header]])) {
            return trim($values[$this->header2Index[$header]], ' "');
        }
        
        return null;
    }
}
